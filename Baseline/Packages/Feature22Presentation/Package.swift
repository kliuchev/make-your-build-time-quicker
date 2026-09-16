// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature22Presentation",
    products: [.library(name: "Feature22Presentation", targets: ["Feature22Presentation"])],
    dependencies: [.package(path: "../Feature22Domain"),
        .package(path: "../Feature22Data")],
    targets: [.target(name: "Feature22Presentation", dependencies: [.product(name: "Feature22Domain", package: "Feature22Domain"), .product(name: "Feature22Data", package: "Feature22Data")])]
)
