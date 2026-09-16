// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature02Data",
    products: [.library(name: "Feature02Data", targets: ["Feature02Data"])],
    dependencies: [.package(path: "../Feature02Domain")],
    targets: [.target(name: "Feature02Data", dependencies: [.product(name: "Feature02Domain", package: "Feature02Domain")])]
)
