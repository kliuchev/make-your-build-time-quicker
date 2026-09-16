// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature26Presentation",
    products: [.library(name: "Feature26Presentation", targets: ["Feature26Presentation"])],
    dependencies: [.package(path: "../Feature26Domain"),
        .package(path: "../Feature26Data")],
    targets: [.target(name: "Feature26Presentation", dependencies: [.product(name: "Feature26Domain", package: "Feature26Domain"), .product(name: "Feature26Data", package: "Feature26Data")])]
)
