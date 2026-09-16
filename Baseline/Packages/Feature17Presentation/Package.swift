// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature17Presentation",
    products: [.library(name: "Feature17Presentation", targets: ["Feature17Presentation"])],
    dependencies: [.package(path: "../Feature17Domain"),
        .package(path: "../Feature17Data")],
    targets: [.target(name: "Feature17Presentation", dependencies: [.product(name: "Feature17Domain", package: "Feature17Domain"), .product(name: "Feature17Data", package: "Feature17Data")])]
)
