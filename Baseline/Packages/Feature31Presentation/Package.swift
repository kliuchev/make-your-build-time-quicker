// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature31Presentation",
    products: [.library(name: "Feature31Presentation", targets: ["Feature31Presentation"])],
    dependencies: [.package(path: "../Feature31Domain"),
        .package(path: "../Feature31Data")],
    targets: [.target(name: "Feature31Presentation", dependencies: [.product(name: "Feature31Domain", package: "Feature31Domain"), .product(name: "Feature31Data", package: "Feature31Data")])]
)
